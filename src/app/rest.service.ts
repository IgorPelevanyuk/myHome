import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import { Timeval } from './timeval';

@Injectable()
export class RestService {
  private baseURL = 'http://159.93.221.24:5001/';
  private tablesURL = 'http://159.93.221.24:5001/tables';

  constructor(private http: HttpClient) { }

  getTables (): Observable<string[]> {
    return this.http.get<string[]>(this.tablesURL);
      //.pipe(
        //tap(heroes => this.log(`fetched heroes`)),
        //catchError(this.handleError('getHeroes', []))
      //);
  }

  getTableData (table_name: string): Observable<Timeval[]> {
    return this.http.get<Timeval[]>(this.baseURL + table_name);
      //.pipe(
        //tap(heroes => this.log(`fetched heroes`)),
        //catchError(this.handleError('getHeroes', []))
      //);
  }

}
