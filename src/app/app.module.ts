import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { ChartModule } from 'angular2-highcharts';
import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';
import { GridsterModule } from 'angular-gridster2';

import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { ValueComponent } from './value/value.component';
import { RestService } from './rest.service';
import { PlotComponent } from './plot/plot.component';

declare var require: any;
export function highchartsFactory() {
  return require('highcharts');
}

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    ValueComponent,
    PlotComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ChartModule,
    GridsterModule
  ],
  providers: [
    RestService,
    {
      provide: HighchartsStatic,
      useFactory: highchartsFactory
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
