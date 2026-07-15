import { Controller, Post, Body } from '@nestjs/common';
import { AgentService } from './agent.service';

@Controller('agent')
export class AgentController {
  constructor(private readonly agentService: AgentService) {}

  @Post('generate')
  async generate(@Body('prompt') prompt: string) {
    return this.agentService.generateUi(prompt);
  }
}
