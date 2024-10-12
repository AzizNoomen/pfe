import { MessageSender } from "../enums/message-sender.enum";

export interface Message {
    text: string;
    sender: MessageSender;
    icon?: string;
}
