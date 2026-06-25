function sleep(milliseconds) {
  const start = new Date().getTime();
  while (new Date().getTime() - start < milliseconds) {}
}

sleep(parseInt(MILLISECONDS || 1000));
