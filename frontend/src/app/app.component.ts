import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend only';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
      this.http.get<{ title: string }>('http://127.0.0.1:8000/api/get_title/').subscribe(data => {
          this.title = data.title;
      });
  }
}
