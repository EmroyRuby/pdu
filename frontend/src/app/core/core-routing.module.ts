import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../auth.guard';
import { LayoutComponent } from './layout/layout/layout.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './account/login/login.component';
import { RegisterComponent } from './account/register/register.component';
import { ProfileComponent } from './account/profile/profile.component';
import { MyEventsComponent } from './events/my-events/my-events.component';
import { EventsCatalogComponent } from './events/events-catalog/events-catalog.component';
import { EventDetailsComponent } from './events/event-details/event-details.component';
import { SignUpComponent } from './events/sign-up/sign-up.component';
import { CreateEventComponent } from './events/create-event/create-event.component';
import { EditProfileComponent } from './account/edit-profile/edit-profile.component';
import { EditEventComponent } from './events/edit-event/edit-event.component';

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
        canActivate: [AuthGuard] 
      }, {
        path: 'profile/edit',
        component: EditProfileComponent,
        canActivate: [AuthGuard] 
      }, {
        path: 'my-events',
        component: MyEventsComponent,
        canActivate: [AuthGuard] 
      },{
        path: 'events',
        component: EventsCatalogComponent
      }, {
        path: 'event',
        component: EventDetailsComponent
      }, {
        path: 'event/sign-up',
        component: SignUpComponent
      }, {
        path: 'event/edit',
        component: EditEventComponent,
        canActivate: [AuthGuard] 
      }, {
        path: 'create-event',
        component: CreateEventComponent,
        canActivate: [AuthGuard] 
      }
    ]
  }, 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class CoreRoutingModule { }