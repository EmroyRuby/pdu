import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  user: any;
  loginForm: FormGroup;
  loginFailed: boolean = false;

  constructor(private fb: FormBuilder, private accountService: AccountService, private router: Router) {
    this.user = this.accountService.getUserData();
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  ngOnInit() {}

  login() {
    if (this.accountService.login(this.loginForm.value.email, this.loginForm.value.password)) {
      this.user = this.accountService.getUserData();
      this.loginFailed = false;
      this.router.navigate(['/profile']);
    } else {
      this.loginFailed = true;
    }
  }
}