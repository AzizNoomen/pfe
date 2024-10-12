import { trigger, state, style, animate, transition } from '@angular/animations';

export const chatbotAnimations = [
    trigger('sendButtonAnimation', [
        state('idle', style({
        opacity: 1,
        transform: 'translateX(0)'
        })),
        state('sent', style({
        opacity: 0,
        transform: 'translateX(30px)'
        })),
        state('stop', style({
        opacity: 1,
        transform: 'translateX(0)'
        })),
        transition('idle => sent', [
        animate('0.3s ease-out')
        ]),
        transition('sent => idle', [
        animate('0s')
        ]),
        transition('sent => stop', [
        animate('0s')
        ])
    ]),
    trigger('slideUpSent', [
        state('void', style({
        opacity: 0,
        transform: 'translateY(50px)'
        })),
        transition(':enter', [
        animate('0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55)', style({
            opacity: 1,
            transform: 'translateY(0)'
        }))
        ])
    ]),
    trigger('loadingThenPopUp', [
        state('void', style({
        opacity: 0,
        transform: 'translateY(20px)'
        })),
        transition(':enter', [
        animate('0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55)', style({
            opacity: 1,
            transform: 'translateY(0)'
        }))
        ])
    ]),
    trigger('slideDown', [
        state('open', style({
            height: '*',
            opacity: 1,
            overflow: 'hidden',
        })),
        state('closed', style({
            height: '0px',
            opacity: 0,
            overflow: 'hidden',
        })),
        transition('closed => open', [
            animate('300ms ease-out')
        ]),
        transition('open => closed', [
            animate('300ms ease-in')
        ]),
    ]),
    trigger('rotateArrow', [
        state('right', style({
            transform: 'rotate(0deg)'
        })),
        state('down', style({
            transform: 'rotate(90deg)'
        })),
        transition('right <=> down', [
            animate('300ms ease-out')
        ])
    ]),
    trigger('rotateIcon', [
        state('default', style({
            transform: 'rotate(0deg)'
        })),
        state('rotated', style({
            transform: 'rotate(360deg)'
        })),
        transition('default <=> rotated', [
            animate('500ms ease-out')
        ])
    ]),
    trigger('popup', [
            state('hidden', style({
            transform: 'scale(0.9)',
            opacity: 0,
        })),
        state('visible', style({
            transform: 'scale(1)',
            opacity: 1,
        })),
        transition('hidden => visible', [
            animate('300ms ease-out')
        ]),
        transition('visible => hidden', [
            animate('300ms ease-in')
        ])
    ]),
    trigger('labelAnimation', [
        state('hidden', style({
        opacity: 0,
        transform: 'translateY(0)'
        })),
        state('visible', style({
            opacity: 1,
            transform: 'translateY(-20px)' // Slide up effect
        })),
        transition('hidden => visible', [
            animate('300ms ease-out')
        ]),
        transition('visible => hidden', [
            animate('300ms ease-in')
        ])
    ])
];
