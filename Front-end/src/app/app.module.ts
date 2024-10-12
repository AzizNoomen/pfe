import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatbotComponent } from './components/chatbot/chatbot.component';
import { FileUploadComponent } from './components/file-upload/file-upload.component';
import { FileUploadService } from './services/file-upload/file-upload.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { NavbarComponent } from './components/navbar/navbar.component';
import { GraphComponent } from './components/graph/graph.component';
import { HomeComponent } from './components/home/home.component';
import { AboutComponent } from './components/about/about.component';


@NgModule({
  declarations: [
    AppComponent,
    FileUploadComponent,
    ChatbotComponent,
    NavbarComponent,
    GraphComponent,
    HomeComponent,
    AboutComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    ProgressSpinnerModule,
    CommonModule,
  ],
  providers: [
    FileUploadService,
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})


export class AppModule { }
