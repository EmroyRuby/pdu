import { Component, Injectable  } from '@angular/core';
import { AccountService } from '../../account/account.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent{

  constructor(private accountService: AccountService, private router: Router) { }

  isLoggedIn(): boolean {
    return this.accountService.isLoggedIn();
  }

  logout(): any {
    this.accountService.logout();
    this.router.navigate(['/login']);
  }

}
