package org.example.videocurator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@org.springframework.scheduling.annotation.EnableScheduling
public class McpServerApplication {
  public static void main(String[] args) {
    if (args.length == 0 || args[0].equals("mcp")) {
      SpringApplication.run(McpServerApplication.class, args);
    } else {
      System.setProperty("spring.ai.mcp.server.enabled", "false");
      try (var context = SpringApplication.run(McpServerApplication.class, args)) {
        int code = org.example.videocurator.cli.AdminCli.run(context, args);
        context.close();
        System.exit(code);
      }
    }
  }
}
