import { NgModule } from '@angular/core';

import { CoreRoutingModule } from './core-routing.module';
import { HomeComponent } from './home/home.component';
import { NavComponent } from './nav/nav.component';
import { LoginComponent } from './login/login.component';
import { EventsCatalogComponent } from './events-catalog/events-catalog.component';
import { RegisterComponent } from './register/register.component';
import { EventDetailsComponent } from './event-details/event-details.component';
import { BrowserModule } from '@angular/platform-browser';
import { LayoutComponent } from './layout/layout.component';
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
    HomeComponent,
    NavComponent,
    LoginComponent,
    RegisterComponent,
    EventsCatalogComponent,
    LayoutComponent,
    EventDetailsComponent
  ]
})
export class CoreModule { }