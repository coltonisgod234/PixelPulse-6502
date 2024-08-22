.segment "CODE"
    font:
        .db #%00110101, #%11111011
    ; Subroutine to refresh display
    refresh_display:
        lda #%00000001    ; Load immediate value %00000001 into accumulator
        sta $3024         ; Store accumulator value into memory address $3024

        ;lda #%00000000    ; Load immediate value %00000000 into accumulator
        ;sta $3024         ; Store accumulator value into memory address $3024
        rts               ; Return from subroutine

    ; Reset subroutine
    rst:
        ldx #$00          ; Initialize X register to 0

    loopy:
        iny               ; Increment Y register
        cpy #$FF          ; Compare Y to 255 (hexadecimal $FF)
        bne loopy         ; Branch back to loopy if Y is not equal to 255
        sta $1000, Y      ; Store accumulator value into memory address $1000 + Y

        jsr refresh_display ; Use JSR to call subroutine
        jmp rst           ; Infinite loop (jump to rst)

    nmi:
        lda #$00          ; Debug statement
        rti               ; Return from interrupt

    irq:
        lda #$10          ; Debug statement
        rti               ; Return from interrupt

.segment "VECTORS"
    .word nmi    ; Non-maskable interrupt vector (address $FFFA)
    .word rst    ; Reset interrupt vector (address $FFFC)
    .word irq    ; Interrupt request vector (address $FFFE)