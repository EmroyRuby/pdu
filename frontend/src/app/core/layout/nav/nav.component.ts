import { Component, Injectable  } from '@angular/core';
import { AccountService } from '../../account/account.service';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent{

  constructor(private accountService: AccountService) { }

  isLoggedIn(): boolean {
    return this.accountService.isLoggedIn();
  }

}
