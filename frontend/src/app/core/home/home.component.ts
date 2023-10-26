import { Component } from '@angular/core';
import { AccountService } from '../account/account.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  constructor(private accountService: AccountService) { }

  isLoggedIn(): boolean {
    return this.accountService.isLoggedIn();
  }
}
