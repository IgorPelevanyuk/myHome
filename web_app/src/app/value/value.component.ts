import { Component, OnInit, Input } from '@angular/core';
import { RestService } from '../rest.service';

import { Timeval } from '../timeval';

@Component({
  selector: 'app-value',
  templateUrl: './value.component.html',
  styleUrls: ['./value.component.css'],
  inputs: ['table']
})
export class ValueComponent implements OnInit {
  @Input() table: string;
  private values: Timeval[];


  constructor(private restService: RestService,) {
  	this.values = [];
  }

  getValues() {
    this.restService.getTableData(this.table).subscribe(values => this.values = values);
  }

  lastValue() {
    return this.values[this.values.length - 1];
  }

  ngOnInit() {
  	this.getValues();
  }

}
