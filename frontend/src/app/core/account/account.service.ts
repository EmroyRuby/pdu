import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { User } from '../models';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private cookieService = inject(CookieService);
  private isAuthenticated: boolean = false;
  private userIdSubject: BehaviorSubject<any> = new BehaviorSubject(null);
  public userId$ = this.userIdSubject.asObservable();

  constructor(private http: HttpClient) {
    // Check if the user is already authenticated based on stored userId in localStorage
    const userId = localStorage.getItem('userId');
    if (userId) {
      this.isAuthenticated = true;
      this.userIdSubject.next(JSON.parse(userId));
    }
  }

  getCsrfToken(){
    return this.cookieService.get("csrftoken");
  }

  // Login method to authenticate user
  async login(email: string, password: string): Promise<boolean> {
    let userData: User = {
      email: email,
      password: password
    };

    this.cookieService.deleteAll('/', 'localhost', true, 'None');

    try {
      const response = await this.http.post<User>(`http://127.0.0.1:8000/api/accounts/login`, userData, {
        withCredentials: true
      }).toPromise();

      const userId = response?.id;

      if (userId) {
        this.isAuthenticated = true;
        this.userIdSubject.next({ userId: userId });
        localStorage.setItem('userId', JSON.stringify({ userId }));
      } else {
        this.isAuthenticated = false;
      }
      return this.isAuthenticated;
    } catch (error) {
      console.error("Error during login:", error);
      return false;
    }
  }

  // Logout method to de-authenticate user
  async logout() {
    try {
      await firstValueFrom(this.http.post<User>(`http://127.0.0.1:8000/api/accounts/logout`, {}).pipe());
      this.cookieService.deleteAll();
      this.isAuthenticated = false;
      this.userIdSubject.next(null);
      localStorage.removeItem('userId');
      console.log("Logout successful");
    } catch (error) {
      console.error("Error during logout:", error);
      throw error;
    }
  }
  

  // Check if the user is logged in
  isLoggedIn(): boolean {
    return this.isAuthenticated;
  }

  // Get user data for the authenticated user
  async getUserData(): Promise<User> {
    try {
      const userData = await firstValueFrom(this.http.get<User>(`http://127.0.0.1:8000/api/accounts/user`, {
        withCredentials: true
      }));
      console.log("User data retrieved successfully");
      return userData;
    } catch (error) {
      console.error("Error during getUserData:", error);
      throw error;
    }
  }

  // Register a new user
  async register(email: string, password: string): Promise<boolean> {
    let userData: User = {
      username: email,
      email: email,
      password: password
    };
  
    try {
      await firstValueFrom(this.http.post<User>(`http://127.0.0.1:8000/api/accounts/register`, userData));
      console.log("Registration successful");
      return await this.login(email, password);
    } catch (error) {
      console.error("Error during registration:", error);
      return false;
    }
  }

  // Update user information
  async updateUser(email: string) {
    try {
      const userData = await firstValueFrom(this.http.put<User>(`http://127.0.0.1:8000/api/accounts/edit`, 
        {email: email}, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
        },
      }));
      console.log("Updated user with id: ", userData.id, ", new data: ", userData);
    } catch (error) {
      console.error("Error during update:", error);
    }
  }

  // Change user password
  async changePassword(old_password: string, new_password: string) {
    try {
      await firstValueFrom(this.http.post(`http://127.0.0.1:8000/api/accounts/password-change`, 
        {old_password: old_password, new_password: new_password}, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
        },
      }));
      console.log("Changed password");
    } catch (error) {
      console.error("Error during password change:", error);
    }
  }

  // Delete the authenticated user's account
  async deleteUser(password: string): Promise<void> {
    try {
      await firstValueFrom(this.http.post<User>(`http://127.0.0.1:8000/api/accounts/delete-account`, 
        {password: password}, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
        },
      }));
      this.isAuthenticated = false;
      this.userIdSubject.next(null);
      localStorage.removeItem('userId');
      this.logout();
      console.log("Account deletion successful");
    } catch (error) {
      console.error("Error during deleteUser:", error);
      throw error;
    }
  }
}
