import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private isAuthenticated: boolean = false;
  private userDataSubject: BehaviorSubject<any> = new BehaviorSubject(null);
  public userData$ = this.userDataSubject.asObservable();

  private autenticatedUsers = [
    {
      email: 'user123@example.com',
      password: 'password123'
    }
  ];

  constructor() {
    const userData = localStorage.getItem('userData');
    if (userData) {
      this.isAuthenticated = true;
      this.userDataSubject.next(JSON.parse(userData));
    }
  }

  login(email: string, password: string): boolean {
    const user = this.autenticatedUsers.find((user) => user.email === email && user.password === password);
    if (user) {
      this.isAuthenticated = true;
      this.userDataSubject.next({ email: email });
      localStorage.setItem('userData', JSON.stringify({ email: email }));
    } else {
      this.isAuthenticated = false;
    }
    return this.isAuthenticated;
  }


  logout(): void {
    this.isAuthenticated = false;
    this.userDataSubject.next(null);
    // Remove user data from local storage when logged out
    localStorage.removeItem('userData');
  }
  
  isLoggedIn(): boolean {
    return this.isAuthenticated;
  }

  getUserData(): any {
    return this.userDataSubject.value;
  }

  register(email: string, password: string): boolean {
    this.autenticatedUsers.push({ email, password });
    this.isAuthenticated = true;
    this.userDataSubject.next({ email: email });
    localStorage.setItem('userData', JSON.stringify({ email: email }));
    return true;
  }

  updateUser(email: string, password: string): void {
    this.autenticatedUsers[this.autenticatedUsers.findIndex((user) => user.email === email)].password = password;
    this.userDataSubject.next({ email: email });
    localStorage.setItem('userData', JSON.stringify({ email: email }));
  }

  deleteUser(email: string): void {
    this.autenticatedUsers.splice(this.autenticatedUsers.findIndex((user) => user.email === email), 1);
    this.isAuthenticated = false;
    this.userDataSubject.next(null);
    localStorage.removeItem('userData');
  }
}