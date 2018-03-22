import { Component, OnInit, Input } from '@angular/core';
import { RestService } from '../rest.service';

import { Timeval } from '../timeval';

@Component({
  selector: 'app-plot',
  templateUrl: './plot.component.html',
  styleUrls: ['./plot.component.css'],
  inputs: ['table']
})

export class PlotComponent implements OnInit {
  @Input() table: string;
  private values: Timeval[];
  options: Object;
  chart: Object;


  constructor(private restService: RestService,) {
    this.values = [];
  }

  saveInstance(chartInstance): void {
    this.chart = chartInstance;
  }

  initChart(values): void {
    console.log('Init chart');
    this.options = {
      chart: { zoomType: 'x' },
      title : { text : this.table },
      xAxis: { type: 'datetime' },
      series: [{
        type: 'area',
        data: values,
      }],
      plotOptions: {
        area: {
          marker: { radius: 2 },
          lineWidth: 1,
          states: {
            hover: { lineWidth: 1 }
          },
          threshold: null
        }
      }
    };
  }

  getValues() {
    this.restService.getTableData(this.table).subscribe(
      //values => this.values = values,
      values => this.initChart(values)
    );
  }

  ngOnInit() {
    this.getValues();

  }

}
