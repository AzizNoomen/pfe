import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  private apiUrl = `${environment.BffUrl}/QnA`;

  constructor(private http: HttpClient) { }

  sendMessage(question: string, generation_model: string, reranker: string): Observable<any> {
    console.log("question", question);
    console.log("generation_model", generation_model);
    console.log("reranker", reranker);
    
    let params = new HttpParams()
      .set('question', question)
      .set('generation_model', generation_model);

    if (reranker && reranker.toLowerCase() !== 'none') {
      params = params.set('reranker', reranker);
    }

    console.log("params", params);
    
    return this.http.get<any>(this.apiUrl, { params: params });
  }
}
