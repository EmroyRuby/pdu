import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { CoreModule } from './core/core.module';
import { AccountService } from './core/account/account.service';

@NgModule({
  declarations: [AppComponent],
  imports: [
    CoreModule
  ],
  providers: [AccountService],
  bootstrap: [AppComponent]
})
export class AppModule { }
