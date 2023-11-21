import { Component } from '@angular/core';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';
import { User } from '../../models';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  user!: User;
  passwordForm: FormGroup;

  constructor(private fb: FormBuilder, private accountService: AccountService, private router: Router) {
    this.passwordForm = this.fb.group({
      password: ['', Validators.required]
    });
  }

  async ngOnInit(){
    this.user = await this.accountService.getUserData();
    console.log(this.user);
  }

  editProfile() {
    this.router.navigate(['/profile/edit']);
  }

  async deleteAccount() {
    await this.accountService.deleteUser(this.passwordForm.value.password);
    this.router.navigate(['/login']);
  }

  logout() {
    this.accountService.logout();
    this.router.navigate(['/login']);
  }

}
