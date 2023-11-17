import { Component } from '@angular/core';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';
import { User } from '../../models';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  user!: User;

  constructor(private accountService: AccountService, private router: Router) {
  }

  async ngOnInit(){
    this.user = await this.accountService.getUserData();
    console.log(this.user);
  }

  editProfile() {
    this.router.navigate(['/profile/edit']);
  }

  deleteAccount() {
    this.accountService.deleteUser();
    this.router.navigate(['/login']);
  }

  logout() {
    this.accountService.logout();
    this.router.navigate(['/login']);
  }

}
