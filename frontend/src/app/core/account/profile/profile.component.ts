import { Component } from '@angular/core';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  user: any;

  constructor(private accountService: AccountService, private router: Router) {
    this.user = this.accountService.getUserData();
  }

  editProfile() {
    this.router.navigate(['/edit-profile']);
  }

  deleteAccount() {
    if (confirm('Are you sure you want to delete your account?')) {
      this.accountService.deleteUser(this.user.email);
      this.router.navigate(['/login']);
    }
  }

  logout() {
    this.accountService.logout();
    this.router.navigate(['/login']);
  }

}
