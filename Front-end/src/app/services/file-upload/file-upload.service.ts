import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpParams, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FileUploadService {
  private uploadUrl = `${environment.BffUrl}/documents`;

  constructor(private http: HttpClient) {}

  uploadFiles(files: File[], chunking_method: string, model_name: string): Observable<HttpEvent<any>> {
    const formData = new FormData();

    files.forEach((file) => {
      formData.append('files', file, file.name);
    });

    console.log('chunking_method in service', chunking_method);
    console.log('model_name in service', model_name);

    let params = new HttpParams()
      .set('chunking_method', chunking_method)
      .set('model_name', model_name);
    console.log('formData', formData);

    const req = new HttpRequest('POST', this.uploadUrl, formData, {
      params: params,
      reportProgress: true
    });

    return this.http.request(req);
  }
}