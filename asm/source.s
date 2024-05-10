.segment "CODE"
    .org $8000
    rst:
        iny
        
        cpy #$FF
        beq rst

        sta $1000,x
        inx
        jmp rst

    nmi:
        rti
    
    irq:
        rti

    .org $fffa
    .word nmi	;Non-maskable interrupt vector
    .word rst	;Reset interrupt vector
    .word irq	;Interrupt request vector