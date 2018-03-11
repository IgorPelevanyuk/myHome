import { Component, OnInit } from '@angular/core';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  tables: string[];

  constructor(private restService: RestService,) { }

  getTables() {
  	this.restService.getTables()
      .subscribe(tables => this.tables = tables);
  }

  ngOnInit() {
  	this.getTables();
  }

}
