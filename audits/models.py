from django.db import models
from django.contrib.auth.models import (BaseUserManager , AbstractBaseUser,AbstractUser,)
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UserManager (BaseUserManager):
    def create_user (self,username, email, nom , prenom , numtel , photo,departement,role, password=None,is_staff=True,is_admin=False):
        if not email:
            raise ValueError('L\'utilisateur doit avoir une adresse email')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            nom = nom,
            prenom = prenom,
            numtel = numtel,
            photo = photo,
            departement = departement,
            role = role,
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        """if role == 1:
            user.admin = True
        else:
            user.admin = False"""
        user.save(using=self._db)
        return user

    def create_superuser (self,username,email, nom , prenom , numtel , photo,departement,role, password=None):
        user = self.create_user(
            username = username,
            email=self.normalize_email(email),
            password=password,
            nom = nom,
            prenom = prenom,
            numtel =   numtel,
            photo= photo,
            departement = departement,
            role = 1,
            is_admin=True,
            is_staff=True,
        )
        user.save(using=self._db)
        return user

    def create_staffuser (self,username, email,nom , prenom , numtel , photo,departement,role, password=None):
        user = self.create_user(
            username = username,
            email=self.normalize_email(email),
            password=password,
            nom = nom,
            prenom = prenom,
            numtel =   numtel,
            photo= photo,
            departement = departement,
            role = role,
            is_staff=True
        )
        user.admin = is_admin
        #user.user_permissions.add(Permission.objects.get(name='Can add audit'))
        user.save(using=self._db)
        return user  

    def __str__(self):
        return self.prenom +''+ self.nom+''+self.role 

class User (AbstractBaseUser):
    ADMINISTRATEUR = 1
    AUDITEUR = 2
    ROLE_CHOICES = (
        (ADMINISTRATEUR, 'Administrateur'),
        (AUDITEUR, 'Auditeur'),
    )
    email = models.EmailField(
    verbose_name='email address',
    max_length=255,
    unique=False,
     )
    username = models.CharField(max_length=20,unique=True, error_messages={ "max_length":"Le username est trop long"})
    nom = models.CharField(max_length=50,null=True, error_messages={ "max_length":"Le nom est trop long"})
    prenom = models.CharField(max_length=50,null=True, error_messages={"max_length":"Le prenom est trop long"})
    departement = models.CharField(blank=True,max_length=50,null=True, error_messages={"max_length":"Le nom du département est trop long"})
    numtel = PhoneNumberField(blank=True,null=True)
    photo = models.ImageField(upload_to='static/Photo_auditeur',null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True,default=2)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nom','prenom','email','numtel' , 'photo','departement','role',]
    

    def __str__(self):
        return str(self.prenom) +'  '+ str(self.nom)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        """if perm in self.get_all_permissions(obj) :
            return True
        else:
            return False"""
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
    @property
    def is_admin(self):
        if self.role == 1 : 
            return True
        else:
            return False
    def auditeurs():
        l=[]
        auditeurs=User.objects.filter(role=2)
        
        for auditeur in auditeurs :
            
            e=[auditeur.username,auditeur.username]
            k=tuple(e)
            l.append(k)
        
        return tuple(l) ;    

    def is_auditeur(self):
        if self.role == 2 :
            return True
        else:
            return False

class Responsable (models.Model):
    photo = models.ImageField(upload_to='static/Photo_responsable')
    nom = models.CharField(max_length=50, error_messages={ "max_length":"Le nom est trop long"})
    prenom = models.CharField(max_length=50, error_messages={"max_length":"Le prenom est trop long"})
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    numeroTel = PhoneNumberField()
    
    def __str__(self):
        return self.prenom + ' ' +self.nom

class Zone (models.Model):
    nom = models.CharField(max_length=50)
    responsable = models.OneToOneField(Responsable,on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return self.nom

class Audit(models.Model):
    AUDITEUR_CHOICES = User.auditeurs()
    date = models.DateTimeField(null=False, auto_now_add=True)
    tauxRespect = models.IntegerField(blank=True,null=True, validators=[MinValueValidator(0),MaxValueValidator(100)])
    tauxMin = models.IntegerField(blank=True,default=75,  validators=[MinValueValidator(0),MaxValueValidator(100)])
    zone = models.OneToOneField(Zone,on_delete = models.CASCADE)
    auditeur = models.CharField(max_length=20,choices=AUDITEUR_CHOICES,unique=True,null=True)

    def __str__(self):  
        return "Audit de la zone "+self.zone.nom+"  "+self.date.strftime("%Y-%m-%d %H:%M:%S")

def get_audit(pk):
    return Audit.objects.get(pk)

class Categorie(models.Model):
    nom = models.TextField()

    def __str__(self):
        return self.nom

class PlanAction(models.Model):
    audit = models.OneToOneField(Audit,on_delete = models.CASCADE, primary_key = True)
    def __str__(self):
        return "plan d'action de l'audit de la zone " +self.audit.zone.nom+" du jour "+ self.audit.date.strftime("%Y-%m-%d %H:%M:%S")

class Action(models.Model):
    probleme = models.TextField(blank=True)
    cause = models.TextField(blank=True)
    actionAfaire = models.TextField(blank=True)
    delai = models.DateTimeField(auto_now_add=True)
    tauxEfficacite = models.IntegerField(blank=True,null=True, validators=[MinValueValidator(0),MaxValueValidator(100)])
    planAction = models.ForeignKey(PlanAction, on_delete=models.CASCADE,related_name='Actions')

    def __str__(self):
        return "action du plan d'action de l'audit du jour "+self.planAction.audit.date.strftime("%Y-%m-%d")

class Standard(models.Model):

    #nom = models.CharField(max_length=100)
    description=models.TextField(max_length=300)
    photoStandard = models.ImageField(upload_to='static/Photo_critère', null=True, blank=True )
    date_de_creation=models.DateField(auto_now_add=True)
    zone=models.ManyToManyField(Zone)
    valstandard=models.IntegerField(blank=True,null=True)
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE, related_name='Categorie')

    def __str__(self):
        return "standard du categorie " + self.categorie.nom

class Score(models.Model):
    
    audit = models.OneToOneField(Audit, on_delete=models.CASCADE, primary_key = True)
    standard = models.OneToOneField(Standard,on_delete=models.CASCADE)
    valeur=models.IntegerField(blank=True, validators=[MinValueValidator(0),MaxValueValidator(100)])
    def __str__(self):
        return "Score Audit de la zone "+self.audit.zone.nom+"  "+self.audit.date.strftime("%Y-%m-%d %H:%M:%S")

