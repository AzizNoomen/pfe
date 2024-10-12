import { trigger, transition, style, animate, state } from '@angular/animations';

export const filesAnimations = [
    trigger('fileAnimation', [
        transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('300ms ease', style({ transform: 'translateX(0)', opacity: 1 }))
        ]),
        transition(':leave', [
        style({ transform: 'translateX(0)', opacity: 1 }),
        animate('400ms ease', style({ transform: 'translateX(-100%)', opacity: 0 }))
        ]),
        
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
]