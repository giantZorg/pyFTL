#            ###
#            # Set Text-fonts
#            textFonts = dict()
#            for size in [8, 16, 32]:
#                textFonts[size] = pygame.font.SysFont(self.parameters['General']['TextFont'], size)
#        
#            # Pause-sprite (to be moved to the sprite generator after testing)
#            pauseSprite = pygame.sprite.Sprite()
#            pauseSprite.image = textFonts[32].render('Pause', False, (254, 254, 254)).convert_alpha()
#            pauseSprite.rect = pauseSprite.image.get_rect()
#            
#            pauseSprite.rect.center = self.screen.get_rect().center
#            pauseSprite.rect.y = self.parameters['General']['PauseOffsetY']
#            
#            drawSpriteGroup.add(pauseSprite)
#            