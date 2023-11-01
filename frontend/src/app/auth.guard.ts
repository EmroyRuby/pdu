import { CanActivateFn } from '@angular/router';
import { AccountService } from './core/account/account.service'; 
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  // Inject your AuthService or authentication service
  const authService = new AccountService(); // Instantiate your AuthService (or use Dependency Injection)
  
  if (authService.isLoggedIn()) {
    return true;
  } else {
    return new Router().createUrlTree(['/login']);; // Deny access to unauthenticated users.
  }
};