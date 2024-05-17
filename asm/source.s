.segment "CODE"
    .org $8000
    rst:
        lda #$FF
        sta $3000
        jmp rst

    nmi:
        rti
    
    irq:
        rti

.segment "VECTORS"
    .word nmi	; Non-maskable interrupt vector
    .word rst	; Reset interrupt vector
    .word irq	; Interrupt request vector