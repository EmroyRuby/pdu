import { NgModule } from '@angular/core';

import { CoreRoutingModule } from './core-routing.module';
import { LayoutComponent } from './layout/layout.component';
import { NavComponent } from './nav/nav.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AccountComponent } from './account/account.component';
import { EventsCatalogComponent } from './events-catalog/events-catalog.component';
import { EventDetailsComponent } from './event-details/event-details.component';
import { CreateEventComponent } from './create-event/create-event.component';
import { RateEventComponent } from './rate-event/rate-event.component';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

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
    AccountComponent,
    EventsCatalogComponent,
    EventDetailsComponent,
    CreateEventComponent,
    RateEventComponent
  ]
})
export class CoreModule { }