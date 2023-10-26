import { NgModule } from '@angular/core';

import { CoreRoutingModule } from './core-routing.module';
import { LayoutComponent } from './layout/layout/layout.component';
import { NavComponent } from './layout/nav/nav.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './account/login/login.component';
import { RegisterComponent } from './account/register/register.component';
import { EventsCatalogComponent } from './events/events-catalog/events-catalog.component';
import { EventDetailsComponent } from './events/event-details/event-details.component';
import { CreateEventComponent } from './events/create-event/create-event.component';
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
    EventsCatalogComponent,
    EventDetailsComponent,
    CreateEventComponent
  ]
})
export class CoreModule { }