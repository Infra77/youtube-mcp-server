package org.example.videocurator.domain;

public class CuratorException extends RuntimeException {
  private final String code;

  public CuratorException(String code, String safeMessage) {
    super(safeMessage);
    this.code = code;
  }

  public String code() {
    return code;
  }
}
