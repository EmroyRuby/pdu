import { TestBed } from '@angular/core/testing';
import { CanActivateFn, Router } from '@angular/router';

import { AuthGuard } from './auth.guard';
import { AccountService } from './core/account/account.service';

describe('AuthGuard', () => {
  let authGuard: AuthGuard;
  let accountService: AccountService;
  let router: Router;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AuthGuard, AccountService, Router]
    });

    authGuard = TestBed.inject(AuthGuard);
    accountService = TestBed.inject(AccountService);
    router = TestBed.inject(Router);
  });

  it('should be created', () => {
    expect(authGuard).toBeTruthy();
  });

  it('should return true if the user is logged in', () => {
    spyOn(accountService, 'isLoggedIn').and.returnValue(true);
    const result = authGuard.canActivate();
    expect(result).toBe(true);
  });

  it('should navigate to login page and return false if the user is not logged in', () => {
    spyOn(accountService, 'isLoggedIn').and.returnValue(false);
    const navigateSpy = spyOn(router, 'navigate');
    
    const result = authGuard.canActivate();
    
    expect(result).toBe(false);
    expect(navigateSpy).toHaveBeenCalledWith(['/login']);
  });
});
