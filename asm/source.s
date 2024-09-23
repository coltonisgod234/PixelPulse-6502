.segment "CODE"
    FONT: 
        .include "font_data.asm"
    dynamic_store:
        ; Store A to the address defined by (X << 8) | Y
        ; This effectively constructs the 16-bit address
        ;STA $0000   ; Store A temporarily (zero page, 1 cycle)
        STY $00     ; Store low byte (Y) to zero page (1 cycle)
        STX $01     ; Store high byte (X) to next zero page (1 cycle)
        ;LDA $0000
        STA ($00),Y ; Store indirect via zero page, uses zero page (5 cycles)
        rts
    
    ; Subroutine to refresh display
    refresh_display:
        pha
        lda #%00000001    ; Load immediate value %00000001 into accumulator
        sta $3024         ; Store accumulator value into memory address $3024

        lda #%00000000    ; Load immediate value %00000000 into accumulator
        sta $3024         ; Store accumulator value into memory address $3024

        pla
        rts               ; Return from subroutine

    ; Reset subroutine
    rst:
        jsr test_display
        ;jsr test_audio
        ;jsr test_controller
        ;jsr draw_text

        jsr refresh_display

        jmp rst

    test_display:
        lda #$00
        ldx #$10
        jsr @col

        @done:
            rts

        @col:
            inx ; Next reigon
            cpx #$2E ; If we have reached the end of VRAM we're done
            bpl @done

            ; Otherwise, call @row
            jsr @row

            jmp @col


        @row:
            iny ; Next coloumn
            dec A

            bcc dynamic_store ; Store those to the screen

            cpy #$FF ; If we need to loop then go back
            bne @row

            rts

        rts
    
    test_audio:
        pha
        phy
        phx

        inc A
        sta $3000
        ;sta $3001
        ;sta $3002

        pla
        ply
        plx

        rts

    draw_text:
        ; A = data, Y = bit index, X = data index
        lda #0
        ldx #0
        ldy #0

        @loop:
            lda FONT_A, x       ; Load data
            asl a               ; Shift left
            and #1              ; Get the LSB

        
        rts


    test_controller:
        ;lda $3011               ; Get our controller #1 state
        ;and #%00000001          ; And with #$01 to isolate the LSB
        ;sta $1050, Y            ; Store that to the screen
        ;asl a                   ; Shift all bits left (go to the next bit)
        ;iny                     ; Increment Y to go to the next position
        ;cpy #$08                ; Balls
        ;bne test_controller     ; Repeat until all bits are done

        lda $3011
        sta $1050

        jsr refresh_display
        rts

    nmi:
        lda #$00          ; Debug statement
        rti               ; Return from interrupt

    irq:
        lda #$10          ; Debug statement
        rti               ; Return from interrupt

.segment "VECTORS"
    .word nmi    ; Non-maskable interrupt vector (address $FFFA)
    .word irq    ; Reset interrupt vector (address $FFFC)
    .word rst    ; Interrupt request vector (address $FFFE)