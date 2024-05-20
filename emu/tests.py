import unittest
import emu

class TestGameController(unittest.TestCase):
    def setUp(self):
        emu.pygame.init()
        self.controller = emu.GameController()

    def test_press_release(self):
        self.assertFalse(self.controller.pressed["up"])
        self.controller.press("up")
        self.assertTrue(self.controller.pressed["up"])
        self.controller.release("up")
        self.assertFalse(self.controller.pressed["up"])

    def test_convert_buttons_to_int(self):
        # Simulate pressing multiple buttons
        self.controller.press("up")
        self.controller.press("left")
        self.controller.press("a")
        self.assertEqual(self.controller.convert_buttons_to_int(), 0b00011010)

    def tearDown(self) -> None:
        emu.pygame.quit()

class TestMemoryAndInstructions(unittest.TestCase):
    def setUp(self):
        emu.pygame.init()
        emu.cpu.memory[0x0000:0x0005] = [0xA9, 0x05, 0x8D, 0x00, 0x15]
    
    def test_get_instruction_from_memory(self):
        instruction = emu.get_instruction_from_memory(0x0000)
        #print("I=", instruction)
        self.assertEqual(instruction, 'LDA #$05')

    def tearDown(self) -> None:
        emu.pygame.quit()
        emu.cpu.memory[0x0000:0x0005] = [0x00,0x00,0x00,0x00,0x00]

class TestWaveGeneration(unittest.TestCase):
    def test_generate_triangle_wave(self):
        wave = emu.generate_triangle_wave(1.0, 440, 1.0)
        self.assertIsInstance(wave, emu.np.ndarray)
        self.assertGreater(len(wave), 0)

    def test_generate_sawtooth_wave(self):
        wave = emu.generate_sawtooth_wave(1.0, 440, 1.0)
        self.assertIsInstance(wave, emu.np.ndarray)
        self.assertGreater(len(wave), 0)

    def test_generate_square_wave(self):
        wave = emu.generate_square_wave(1.0, 440, 1.0)
        self.assertIsInstance(wave, emu.np.ndarray)
        self.assertGreater(len(wave), 0)

    def test_generate_sine_wave(self):
        wave = emu.generate_sine_wave(1.0, 440, 1.0)
        self.assertIsInstance(wave, emu.np.ndarray)
        self.assertGreater(len(wave), 0)

class TestUpdateIOFunction(unittest.TestCase):
    def setUp(self):
        emu.cpu.memory[0x0000:0x0005] = [
            0xA9, 0x0F,  # LDA #$0F
            #0x8D, 0x00, 0x80  # STA $8000
        ]
        emu.cpu.pc = 0

    def test_load(self):
        emu.cpu.step()  # Step 1: Execute LDA #$0F
        emu.cpu.step()  # Step 2: Prepare for STA $8000
        self.assertEqual(emu.cpu.acc, 0x0F)

    #def test_store(self):
    #    emu.cpu.step()  # Step 1: Execute LDA #$0F
    #    emu.cpu.step()  # Step 2: Execute STA $8000
    #    emu.cpu.step()  # Step 3: Move to next instruction
    #    emu.assertEqual(emu.cpu.memory[0x1000], 0x0F)

    #def test_store(self):
    #    emu.cpu.step()
    #    emu.cpu.step()
    #    emu.cpu.step() # 3 Cylces For STA

    #def test_update(self):
    #    emu.updateIO()
    #    #parray = emu.pygame.PixelArray(emu.display)
    #    #self.assertEqual(parray[0, 0], (255,255,255))

if __name__ == "__main__":
    unittest.main()