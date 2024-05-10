import new as console

#def debug_console():
#    #print("*** DBG CONSOLE ***")
#    command = input("> ")
#    cmd_ops = command.split(" ")
#    if command == "help":
#        print("Avalible commands, step, trace, memsearch, peek, poke, freeze, rewind, disassemble")
#    elif command == "step" or command == "s":
#        cpu.step()
#        update_io()
#        pygame.display.flip()
#        dbg_trace.append([cpu.memory[cpu.pc], cpu.pc])  # Logging program counter (PC) value
#
#        if cpu.memory[cpu.pc] == 0x00:
#            print("The Instruction Was BRK, That Means The Program Should Have Ended, But It Will Continue In Debug Mode")
#
#        print("Stepped 1 Step")
#    elif cmd_ops[0] == "trace" or cmd_ops[0] == "t":
#        print(dbg_trace)
#    elif cmd_ops[0] == "memsearch" or cmd_ops[0] == "m":
#        for address in len(cpu.memory):
#            try:
#                if cpu.memory[address] == cmd_ops[1]:
#                    print(address, end=" ")
#                else: print(address)
#            except IndexError:
#                print("No arugment specified")
#                return
#    elif cmd_ops[0] == "peek":
#        try:
#            print(cpu.memory[cmd_ops[1]])
#        except IndexError:
#            print("Invalid Address")
#    elif cmd_ops[0] == "poke":
#        try:
#            cpu.memory[cmd_ops[1]] = cmd_ops[2]
#        except IndexError:
#            print("Invalid Address")
#    elif cmd_ops[0] == "rewind":
#        try:
#            cpu.pc = cmd_ops[1]
#        except Exception:
#            print("Error Rewinding PC")
#    elif cmd_ops[0] == "disassemble" or cmd_ops[0] == "d":
#        addr_parser = py65.disassembler.AddressParser()
#        dasm = py65.disassembler.Disassembler(cpu, addr_parser)
#
#        i = dasm.instruction_at(cpu.pc)
#
#        inst_fmt_opc = i[1]
#        inst_fmt_opr = i[0]
#
#        print(f"{inst_fmt_opc: <3} {hex(inst_fmt_opr)}")
#    elif cmd_ops[0] == "disassembletrace" or cmd_ops[0] == "dt":
#        for j in range(len(dbg_trace)):
#            addr_parser = py65.disassembler.AddressParser()
#            dasm = py65.disassembler.Disassembler(cpu, addr_parser)
#
#            i = dasm.instruction_at(dbg_trace[j][0])
#
#            inst_fmt_opc = i[1]
#            inst_fmt_opr = i[0]
#
#            print(f"{inst_fmt_opc: <3} {hex(inst_fmt_opr)}", end=" | ")
#        print("")
#    else:
#        print("Invalid Command")

print("    OK.")
command = input(".")

args = command.split(" ")

if command == "help":
    print("commands: mem, search, step, s, disassemble, d, quit, press, release, peek, poke, bpeek, bpoke, trace, t")

elif command == "search":
    for byte in len(console.cpu.memory):
        if console.cpu.memory[byte] == args[1]:
            print(byte)