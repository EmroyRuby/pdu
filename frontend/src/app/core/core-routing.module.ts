import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { authGuard } from '../auth.guard';
import { LayoutComponent } from './layout/layout/layout.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './account/login/login.component';
import { RegisterComponent } from './account/register/register.component';
import { ProfileComponent } from './account/profile/profile.component';
import { EventsCatalogComponent } from './events/events-catalog/events-catalog.component';
import { EventDetailsComponent } from './events/event-details/event-details.component';
import { SignUpComponent } from './events/sign-up/sign-up.component';
import { CreateEventComponent } from './events/create-event/create-event.component';

const routes: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [
      {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
      }, {
        path: 'home',
        component: HomeComponent
      }, {
        path: 'login',
        component: LoginComponent
      }, {
        path: 'register',
        component: RegisterComponent
      }, {
        path: 'profile',
        component: ProfileComponent,
        canActivate: [authGuard] 
      }, {
        path: 'events',
        component: EventsCatalogComponent
      }, {
        path: 'events/event',
        component: EventDetailsComponent
      }, {
        path: 'events/event/sign-up',
        component: SignUpComponent
      }, {
        path: 'create-event',
        component: CreateEventComponent,
        canActivate: [authGuard] 
      }
    ]
  }, 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class CoreRoutingModule { }