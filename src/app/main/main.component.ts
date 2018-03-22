import { Component, OnInit } from '@angular/core';
import { RestService } from '../rest.service';
import { GridsterConfig, GridsterItem }  from 'angular-gridster2';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})

export class MainComponent implements OnInit {
  tables: string[];
  options: GridsterConfig;
  dashboard: Array<GridsterItem>;

  static itemChange(item, itemComponent) {
    console.info('itemChanged', item, itemComponent);
  }

  static itemResize(item, itemComponent) {
    console.info('itemResized', item, itemComponent);
  }

  constructor(
    private restService: RestService,
  ) { }

  getTables() {
  	this.restService.getTables()
      .subscribe(tables => this.tables = tables);
  }

  ngOnInit() {
  	this.getTables();
    this.options = {
      minCols: 2,
      minRows: 2,
      itemChangeCallback: MainComponent.itemChange,
      itemResizeCallback: MainComponent.itemResize,
      displayGrid: 'onDrag&Resize',
      fixedColWidth: 250, // fixed col width for gridType: 'fixed'
      fixedRowHeight: 250,
      margin: 10,
      draggable: { enabled: true },
    };
    this.dashboard = [
      {cols: 1, rows: 1, y: 0, x: 0, table_name: "01_01"},
      {cols: 1, rows: 1, y: 0, x: 1, table_name: "01_02"}
    ];
  }

  changedOptions() {
    this.options.api.optionsChanged();
  }

  removeItem(item) {
    this.dashboard.splice(this.dashboard.indexOf(item), 1);
  }

  addItem() {
    this.dashboard.push({});
  }

}
