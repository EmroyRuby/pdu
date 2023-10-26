import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl  } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  showAlert = false;

  constructor(private fb: FormBuilder, private accountService: AccountService, private router: Router) {
    this.registerForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  passwordMatchValidator(control: AbstractControl) {
    const passwordControl = control.get('password');
    const confirmPasswordControl = control.get('confirmPassword');
  
    if (passwordControl && confirmPasswordControl) {
      const password = passwordControl.value;
      const confirmPassword = confirmPasswordControl.value;
  
      if (password === confirmPassword) {
        return null;
      } else {
        return { passwordMismatch: true };
      }
    } else {
      return null;
    }
  }
  

  register() {
    if (this.registerForm.valid) {
      if (this.accountService.register(this.registerForm.value.email, this.registerForm.value.password)) {
        this.accountService.register(this.registerForm.value.email, this.registerForm.value.password);
        this.accountService.login(this.registerForm.value.email, this.registerForm.value.password)
        this.router.navigate(['/profile']);
      }else {
          this.showAlert = true;
        
      }
    }
  }
}