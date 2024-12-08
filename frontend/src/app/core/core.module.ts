import { NgModule } from '@angular/core';

import { CoreRoutingModule } from './core-routing.module';
import { LayoutComponent } from './layout/layout/layout.component';
import { NavComponent } from './layout/nav/nav.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './account/login/login.component';
import { RegisterComponent } from './account/register/register.component';
import { MyEventsComponent } from './events/my-events/my-events.component';
import { EventsCatalogComponent } from './events/events-catalog/events-catalog.component';
import { EventDetailsComponent } from './events/event-details/event-details.component';
import { SignUpComponent } from './events/sign-up/sign-up.component';
import { CreateEventComponent } from './events/create-event/create-event.component';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { EditEventComponent } from './events/edit-event/edit-event.component';
import { ProfileComponent } from './account/profile/profile.component';
import { EditProfileComponent } from './account/edit-profile/edit-profile.component';
import { HelpComponent } from './account/help/help.component';  // Add this import


@NgModule({
  imports: [
    BrowserModule,
    CoreRoutingModule, 
    FormsModule,
    ReactiveFormsModule
  ],
  exports: [
    CoreRoutingModule,
    NavComponent,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    LayoutComponent,
    NavComponent,
    HomeComponent,
    RegisterComponent,
    LoginComponent,
    ProfileComponent,
    EditProfileComponent,
    MyEventsComponent,
    EventsCatalogComponent,
    EventDetailsComponent,
    EditEventComponent,
    SignUpComponent,
    CreateEventComponent,
    HelpComponent
  ]
})
export class CoreModule { }