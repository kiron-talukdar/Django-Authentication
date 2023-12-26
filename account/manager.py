from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user (self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Username must be set')
        if not email:
            raise ValueError('Email must be set')
        
       
        email=self.normalize_email(email)   #normalize the email, its come from BaseUserManager
        #create user,,,,    "self.model" is user model
        user=self.model(username=username,email=email,**extra_fields,)
        user.set_password(password)         # set_password to Hash password
        user.save(using=self._db)           # save data in default database "self._db"
        return user


    def create_superuser(self, username, email, password, **extra_fields):
        #call create_user method
        user=self.create_user(username=username,email=email,password=password,*extra_fields,)

        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self._db)           # save data in default database "self._db"
        return user
