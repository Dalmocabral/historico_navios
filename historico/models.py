from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Colaborador(models.Model):
    
    CARGO_CHOICES = [
        ('GER', 'Gerente'),
        ('CORD', 'Coordenador'),
        ('SUP', 'Supervisor'),        
        ('AUX', 'Auxiliar'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="colaborador")    
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20, unique=True)    
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato: 000.000.000-00'
            )
        ]
    )
    
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=6, choices=CARGO_CHOICES)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.matricula})"

    def save(self, *args, **kwargs):
        # Se for um novo Colaborador (não existe no banco)
        if not self.pk:
            # Limpa o CPF (remove pontos e traço)
            cpf_limpo = ''.join(filter(str.isdigit, self.cpf))
            senha = cpf_limpo[:6]  # Primeiros 6 dígitos

            # Cria o User associado
            user = User.objects.create_user(
                username=self.matricula,
                email=self.email,
                password=senha,
                first_name=self.nome,
                last_name=self.sobrenome
            )
            self.user = user  # Associa o User ao Colaborador

        # Chama o método save original para salvar o Colaborador
        super().save(*args, **kwargs)

# Sinal para atualizar o User quando o Colaborador for atualizado
@receiver(post_save, sender=Colaborador)
def update_user_for_colaborador(sender, instance, **kwargs):
    """
    Sinal para atualizar o User quando um Colaborador for atualizado
    """
    # Verificar se o User já existe (não é uma nova instância)
    if instance.user_id:
        instance.user.username = instance.matricula
        instance.user.email = instance.email
        instance.user.first_name = instance.nome
        instance.user.last_name = instance.sobrenome
        instance.user.save()