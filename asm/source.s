.segment "CODE"
    .org $fffa
    .word nmi	;Non-maskable interrupt vector
    .word rst	;Reset interrupt vector
    .word irq	;Interrupt request vector

    .org $8000
    rst:
        lda #$0F
        sta $1000
        jmp rst

    nmi:
        rti
    
    irq:
        rti