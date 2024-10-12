import { AfterViewChecked, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { chatbotAnimations } from '../../animations/chatbot.animations';
import { ERROR_MESSAGE, ICON_PATHS, INTRO_TEXT, PLACEHOLDER_TEXT } from '../../constants/chatbot.constant';
import { AnimationState } from '../../enums/animation-state.enum';
import { ButtonState } from '../../enums/button-state.enum';
import { DropdownOption1, DropdownOption2 } from '../../enums/chatbot_dropdowns.enum';
import { MessageSender } from '../../enums/message-sender.enum';
import { Message } from '../../interfaces/chatbot.interface';
import { ChatbotService } from '../../services/chatbot/chatbot.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
  animations: [chatbotAnimations]
})


export class ChatbotComponent implements AfterViewChecked, OnInit {
  messages: Message[] = [];
  userMessage: string = '';
  loading: boolean = false;
  sendButtonState: ButtonState = ButtonState.Idle;
  messageProcessing: boolean = false;
  private typingIntervalId: any;
  introText: string = INTRO_TEXT;
  introTextAnimated: string = '';
  showIntroText: boolean = true;
  introTextComplete: boolean = false;
  userMessagePlaceholder: string = PLACEHOLDER_TEXT;
  
  dropdownOpen1 = false;
  dropdownOpen2 = false;
  selectedOption1: string | null = 'Llama3.1 8B';
  selectedOption2: string | null = 'None';
  dropdownOptions1 = Object.values(DropdownOption1);
  dropdownOptions2 = Object.values(DropdownOption2);
  showSettings = false;
  iconRotated = false;
  settingsVisible = false;

  animationState: AnimationState = AnimationState.Idle;

  @ViewChild('messagesContainer', { static: false }) messagesContainer!: ElementRef;
  
  constructor(private chatbotService: ChatbotService) {}

  sendMessage() {
    if (this.userMessage.trim() === '' || this.messageProcessing) {
      return;
    }
  
    this.messageProcessing = true;
    this.sendButtonState = ButtonState.Sent;
    this.animationState = AnimationState.Sent;

    const modelName = this.selectedOption1?.split(' ')[0].toLowerCase() + ':latest';
    const reranker = this.selectedOption2?.toLowerCase();

    console.log

    const userMsg: Message = { text: this.userMessage, sender: MessageSender.User, icon: ICON_PATHS.userIcon };
    this.messages.push(userMsg);
    
    setTimeout(() => {
      this.loading = true;
    }, 1500);
  
    this.chatbotService.sendMessage(this.userMessage, modelName, reranker!).subscribe(
      response => {
        this.handleSuccessfulResponse(response);
      },
      error => {
        this.handleErrorResponse(error);
      }
    );
  
    this.userMessage = '';
    this.sendButtonState = ButtonState.Idle;
    this.animationState = AnimationState.Idle;
  }
  
  private handleSuccessfulResponse(response: string) {
    this.updatePreviousIcon();
    this.loading = false;
    this.typeMessage(response);
  }

  private handleErrorResponse(error: any) {
    console.error('Error sending message:', error);
    this.loading = false;
    const errorMsg: Message = { text: ERROR_MESSAGE, sender: MessageSender.Bot, icon: ICON_PATHS.botIconIdle };
    this.updatePreviousIcon();
    this.messages.push(errorMsg);
    this.sendButtonState = ButtonState.Idle;
    this.messageProcessing = false;
    this.scrollToBottom();
  }

  private typeMessage(message: string) {
    let index = 0;
    const botMsg: Message = { text: '', sender: MessageSender.Bot, icon: ICON_PATHS.botIcon };
    this.messages.push(botMsg);

    this.sendButtonState = ButtonState.Stop;
    this.animationState = AnimationState.Stop;

    this.typingIntervalId = setInterval(() => {
      if (index < message.length) {
        botMsg.text = message.substring(0, index + 1);
        index++;
      } else {
        clearInterval(this.typingIntervalId);
        this.sendButtonState = ButtonState.Idle;
        this.animationState = AnimationState.Idle;
        this.updatePreviousIcon();
        this.messageProcessing = false;
        this.scrollToBottom();
      }
    }, 50);
  }

  private updatePreviousIcon() {
    const lastIndex = this.messages.length - 1;
    if (lastIndex >= 0) {
      if (this.messages[lastIndex].sender === MessageSender.User) {
        this.messages[lastIndex].icon = ICON_PATHS.userIconIdle;
      } else if (this.messages[lastIndex].sender === MessageSender.Bot) {
        this.messages[lastIndex].icon = ICON_PATHS.botIconIdle;
      }
    }
  }

  stopTyping() {
    if (this.typingIntervalId) {
      clearInterval(this.typingIntervalId);
      this.typingIntervalId = null;
      this.sendButtonState = ButtonState.Idle;
      this.animationState = AnimationState.Idle;
      this.updatePreviousIcon();
      this.messageProcessing = false;
    }
  }

  scrollToBottom(): void {
    try {
      this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error(err);
    }
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  ngOnInit(): void {
    this.typeIntroText();
  }

  private typeIntroText() {
    let index = 0;
    const intervalId = setInterval(() => {
      if (index < this.introText.length) {
        this.introTextAnimated = this.introText.substring(0, index + 1);
        index++;
      } else {
        clearInterval(intervalId);
        this.introTextComplete = true;
      }
    }, 50);
  }

  toggleDropdown(dropdown: number) {
    if (dropdown === 1) {
      this.dropdownOpen1 = !this.dropdownOpen1;
    } else if (dropdown === 2) {
      this.dropdownOpen2 = !this.dropdownOpen2;
    }
  }

  selectOption(option: string, dropdown: number) {
    if (dropdown === 1) {
      this.selectedOption1 = option;
      this.dropdownOpen1 = false;
    } else if (dropdown === 2) {
      this.selectedOption2 = option;
      this.dropdownOpen2 = false;
    }
  }

  openSettings() {
    this.dropdownOpen1 = false;
    this.dropdownOpen2 = false;
    this.showSettings = true;
    setTimeout(() => this.settingsVisible = true, 300); // Show immediately
    this.iconRotated = !this.iconRotated;
  }

  closeSettings() {
    this.settingsVisible = false;
    setTimeout(() => this.showSettings = false, 300); // Delay to match animation
  }
}
