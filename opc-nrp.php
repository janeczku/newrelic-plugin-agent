<?php
/**
 * PHP OPC Stats for NewRelic Plugin Agent
 */

class Status {

  public $result = [];

  public function __construct() {
    //
  }

  public function configuration() {
    $raw = opcache_get_configuration();
    $this->result['config'] = $raw;
  }

  // Returns a json_encoded array of opcache status
  public function status() {

    // Guard execution if the extension is not loaded.
    if (! extension_loaded("Zend OPcache")) {
      return json_encode([]);
    }

    // Clear out data from prevous run
    $this->result['status'] = null;
    $raw = \opcache_get_status($with_scripts);
    $this->result['status'] = $raw;
    return json_encode($this->result);
  }
}

$opcache = new Status;
echo $opcache->status();
