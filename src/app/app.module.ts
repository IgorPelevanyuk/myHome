import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';


import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { ValueComponent } from './value/value.component';
import { RestService } from './rest.service';


@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    ValueComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [RestService],
  bootstrap: [AppComponent]
})
export class AppModule { }
