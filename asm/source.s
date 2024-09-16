.segment "CODE"
    ; Subroutine to refresh display
    refresh_display:
        pha
        lda #%00000001    ; Load immediate value %00000001 into accumulator
        sta $3024         ; Store accumulator value into memory address $3024

        ;lda #%00000000    ; Load immediate value %00000000 into accumulator
        ;sta $3024         ; Store accumulator value into memory address $3024
        pla
        rts               ; Return from subroutine

    ; Reset subroutine
    rst:
        ;jsr test_display
        jsr test_audio
        ;jsr test_controller
        ;jsr draw_text
        jmp rst

    delay_loop_1:
        ; Push stuff
        php
        pha
        phx
        phy

        ldy #$00
        @Loop:
            iny

            cpy #$15
            bne @Loop

            rts

        plp
        pla
        plx
        ply

        rts


    test_display:
        inx               ; Increment X register

        inc a
        
        ; Left side
        sta $1000, X      ; Store accumulator value into memory address $1000 + X

        cpx #$FF          ; Compare X to 255 (hexadecimal $FF)
        bne test_display  ; Branch back to loopy if X is not equal to 255

        jsr refresh_display
        rts
    
    test_audio:
        inc A
        sta $3005

        jsr refresh_display

        rts

    draw_text:
        ; A = data, Y = bit index, X = data index
        lda #0
        ldx #0
        ldy #0

        @loop:
            ;lda FONT_A, x       ; Load data
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