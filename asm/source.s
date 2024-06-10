.segment "CODE"
    ;.org $8000
    rst:
        dex
        stx $3000
        jmp rst

    nmi:
        lda #$00 ; Debug statement
        rti
    
    irq:
        lda #$10 ; Debug statement
        rti

.segment "VECTORS"
    .word nmi    ; Non-maskable interrupt vector (address $FFFA)
    .word rst    ; Reset interrupt vector (address $FFFC)
    .word irq    ; Interrupt request vector (address $FFFE)