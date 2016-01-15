#pragma once
/**
 *  @file connect.h
 *  @date 12.12.2014
 *  @author mkoenig
 *  @brief 
 *
 *  $LastChangedDate$
 *  $LastChangedBy$
 *  $LastChangedRevision$
 *
 */

#include "pydbc/connection.h"
#include <string>

namespace pydbc {

/**
 * @brief Establish a new connection to the database identified by the given
 *        data source name
 * @param connection_string The connection string to connect with the database
 */
connection connect(std::string const & connection_string);

}
