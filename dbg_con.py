#from typing import Any
#from main import cpu, screen
#import pygame
#from time import sleep, monotonic
#
#pygame.quit()
#
#breakpoints = {}
#traces = []
#frame_counter = 0
#
#def step():
#    global frame_counter
#    # Handle The Pygame Things
#    #for event in pygame.event.get():
#    #    if event.type == pygame.QUIT: exit(0)
#
#    # Poll For Input
#    #keys = pygame.key.get_pressed()
#    #for key, button in main.key_mappings.items():
#    #    if keys[key]:
#    #        main.controller1.press(button)
#    #    else:
#    #        main.controller1.release(button)
#    
#    # Start timing (To get a delta time)
#    instruction_execution_start = monotonic()
#
#    # Execute The Instruction
#    cpu.step()
#    regs = {"a":cpu.a,
#            "x":cpu.x,
#            "y":cpu.y,
#            "pc":cpu.pc,
#            "p":cpu.p,
#            "sp":cpu.sp,
#            "disassembled":get_instruction_from_memory(cpu.pc)
#    }
#    traces.append(regs)
#
#    # Calculate the delta time
#    instruction_execution_detla = monotonic() - instruction_execution_start
#
#    #print(f"[DEBUG] START:{instruction_execution_start}, DELTA:{instruction_execution_detla}")
#
#    # Check if the instruction is a break (BRK instruction)
#    if cpu.memory[cpu.pc] == 0x00:
#        print("Encountered BRK instruction.")
#
#    #main.display.fill((0, 0, 0))
#
#    #pygame.display.flip()
#
#    frame_counter += 1
#    if frame_counter == 1024:
#        frame_counter = 0
#        #main.update_io()
#
#    sleep(instruction_execution_detla)
#
#def step_pygame():
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT: exit(0)
#        display.fill((0, 0, 0))
#        pygame.display.flip()
#
#def dbg_console():
#    # Commands: (s:step|t:trace|bp:breakpoint|rmbp:remove_breakpoint|r:registers|ec:execute-custom|q:quit|rbp:run-until-bp|d:disassemble|lbp:list-bps)
#    cmd = input(".").lower().split()
#    if cmd[0] in ["q", "quit", "exit"]:
#        quit(0)
#    if cmd[0] in ["s", "step"]:
#        print("AC | RX | RY | PC   |   NV-BDIZC | SP | IR")
#        print(f"{cpu.a:02X} | {cpu.x:02X} | {cpu.y:02X} | {cpu.pc:02X} | {bin(cpu.p):<10} | {cpu.sp:02X} | {get_instruction_from_memory(cpu.pc):<13}")
#        step()
#
#    if cmd[0] in ["r", "registers"]:
#        print("AC | RX | RY | PC   |   NV-BDIZC | SP | IR")
#        print(f"{cpu.a:02X} | {cpu.x:02X} | {cpu.y:02X} | {cpu.pc:02X} | {bin(cpu.p):<10} | {cpu.sp:02X} | {get_instruction_from_memory(cpu.pc):<13}")
#
#    if cmd[0] in ["d"]:
#        print(main.get_instruction_from_memory(cpu.pc))
#    
#    if cmd[0] in ["bp"]:
#        if cmd[1] in breakpoints.keys():
#            print(f"A breakpoint with the name {cmd[1]} already exists")
#            return 1
#        else:
#            breakpoints[cmd[1]] = cmd[2]
#    
#    if cmd[0] in ["lbp", "list-bps", "bps"]:
#        print("Name           Value")
#        print("--------------------")
#        for key, value in breakpoints.items():
#            print(f"{key: <15}{value: <15}")
#
#    if cmd[0] in ["rbp"]:
#        print("Stepping until breakpoint")
#        while str(cpu.pc) not in breakpoints.values():
#            step()
#            print(f"{cpu.a:02X} | {cpu.x:02X} | {cpu.y:02X} | {cpu.pc:02X} | {bin(cpu.p):<10} | {cpu.sp:02X} | {get_instruction_from_memory(cpu.pc):<13}")
#
#        # We hit something, but we wanna know what
#        for key, value in breakpoints.items():
#            if value == str(cpu.pc): # If the value is the same as the program counter. Conversion to string is nessasary as breakpoints.items() contains strings no matter the type
#                print(f"Hit breakpoint '{key}' at address {value}!") # Tell the user
#                return 0
#            
#    if cmd[0] in ["t", "trace"]:
#        print("AC    | RX    | RY    | PC    |   NV-BDIZC | SP    | IR")
#        for trace in traces:
#            print(f"{trace["a"]: <5} | {trace["x"]: <5} | {trace["y"]: <5} | {trace["pc"]: <5} | {bin(trace["p"]): <8} | {trace["sp"]: <5} | {trace["disassembled"]: <13}")
#
#
#while True: 
#    try:
#        dbg_console()
#    except KeyboardInterrupt:
#        pass
#    except Exception as e:
#        print("exception", e)